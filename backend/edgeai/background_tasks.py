"""
后台任务管理
定期同步远程集群状态到本地数据库
"""
import asyncio
import logging
from datetime import datetime
from typing import Optional
import httpx
import sys
from pathlib import Path

# Add project root to path for imports
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config.remote_api import REMOTE_API_CONFIG, get_remote_api_url
from database.edgeai import get_db, Node, Cluster

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 全局标志，用于控制后台任务的运行
_background_task_running = False
_background_task: Optional[asyncio.Task] = None


async def sync_cluster_status_from_remote():
    """
    从远程API同步集群状态到本地数据库
    """
    try:
        logger.info("Starting cluster status sync from remote API")

        # 获取远程集群状态
        url = get_remote_api_url("MONITOR_CLUSTER_STATUS")
        timeout = REMOTE_API_CONFIG["TIMEOUT"]

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            remote_status = response.json()

        logger.debug(f"Remote cluster status: {remote_status}")

        # 更新本地数据库
        db = next(get_db())
        try:
            # 获取远程节点信息
            remote_nodes = remote_status.get("nodes", [])

            for remote_node in remote_nodes:
                node_ip = remote_node.get("ip")
                if not node_ip:
                    continue

                # 在本地数据库中查找对应的节点
                local_node = db.query(Node).filter(Node.path_ipv4 == node_ip).first()

                if local_node:
                    # 更新节点状态
                    remote_state = remote_node.get("state", "idle")
                    remote_cpu = remote_node.get("cpu_usage", 0.0)
                    remote_memory = remote_node.get("memory_usage", 0.0)

                    # 映射远程状态到本地状态
                    if remote_state == "running":
                        local_node.state = "online"
                    elif remote_state == "idle":
                        local_node.state = "idle"
                    elif remote_state == "training":
                        local_node.state = "training"
                    else:
                        local_node.state = "offline"

                    # 更新资源使用情况
                    local_node.cpu_usage = remote_cpu
                    local_node.memory_usage = remote_memory
                    local_node.last_updated_time = datetime.now()

                    logger.debug(f"Updated node {node_ip}: state={local_node.state}, cpu={remote_cpu}%, mem={remote_memory}%")

            db.commit()
            logger.info(f"Successfully synced {len(remote_nodes)} nodes from remote API")

        except Exception as e:
            db.rollback()
            logger.error(f"Error updating local database: {e}")
        finally:
            db.close()

    except httpx.HTTPError as e:
        logger.warning(f"Failed to fetch remote cluster status: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in cluster status sync: {e}")


async def periodic_sync_task(interval_seconds: int = 60):
    """
    定期同步任务主循环

    Args:
        interval_seconds: 同步间隔（秒），默认60秒
    """
    global _background_task_running

    logger.info(f"Starting periodic sync task (interval: {interval_seconds}s)")
    _background_task_running = True

    while _background_task_running:
        try:
            # 执行同步任务
            await sync_cluster_status_from_remote()

            # 等待下一次同步
            await asyncio.sleep(interval_seconds)

        except asyncio.CancelledError:
            logger.info("Periodic sync task cancelled")
            break
        except Exception as e:
            logger.error(f"Error in periodic sync task: {e}")
            # 发生错误后等待一段时间再重试
            await asyncio.sleep(interval_seconds)

    logger.info("Periodic sync task stopped")


async def start_background_tasks(sync_interval: int = 60):
    """
    启动后台任务

    Args:
        sync_interval: 同步间隔（秒），默认60秒
    """
    global _background_task, _background_task_running

    if _background_task and not _background_task.done():
        logger.warning("Background task is already running")
        return

    logger.info(f"Starting background tasks with {sync_interval}s sync interval")

    # 创建后台任务
    _background_task = asyncio.create_task(periodic_sync_task(sync_interval))

    logger.info("Background tasks started successfully")


async def stop_background_tasks():
    """
    停止后台任务
    """
    global _background_task, _background_task_running

    logger.info("Stopping background tasks...")

    _background_task_running = False

    if _background_task and not _background_task.done():
        _background_task.cancel()
        try:
            await _background_task
        except asyncio.CancelledError:
            pass

    logger.info("Background tasks stopped successfully")


def is_background_task_running() -> bool:
    """
    检查后台任务是否正在运行

    Returns:
        True if running, False otherwise
    """
    return _background_task_running and _background_task and not _background_task.done()
