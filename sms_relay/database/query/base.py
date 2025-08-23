
import logging
import time
from datetime import datetime, timedelta
from typing import Generic, TypeVar

from settings.connection_settings import DBConnectionSettings
from sqlalchemy import create_engine, exc, text
from sqlalchemy.orm import Session

Maybe = TypeVar("Maybe")

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

# Uncomment the following to log SQL queries
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

class MaybeConnected(Generic[Maybe]):
    def __init__(self, value: Maybe = None, error: Exception = None):
        self.value = value
        self.error = error

    def is_okay(self) -> bool:
        return self.error is None

    def is_error(self) -> bool:
        return self.error is not None


class Connection:
    def __init__(
        self,
        pool_size: int = 5,
        max_overflow: int = 10,
        wait_for_server_time: timedelta = timedelta(minutes=2),
        retry_time: timedelta = timedelta(seconds=10),
    ):
        self.wait_for_server_time = wait_for_server_time
        self.retry_time = retry_time
        self.engine = create_engine(
            DBConnectionSettings().url,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.verify_can_connect()
    
    def verify_can_connect(self):
        start_time = datetime.now()
        result = self.attempt_connection(start_time)
        if result.is_okay():
            logger.info(
                "Connection now available after %s seconds",
                (datetime.now() - start_time).total_seconds(),
            )
        
        if result.is_error():
            self.engine.dispose()
            raise ValueError(
                f"Unable to connect to database {DBConnectionSettings().url} after {self.wait_for_server_time.seconds} seconds."
            ) from result.error

    def attempt_connection(
        self,
        start_time: datetime,
    ) -> MaybeConnected:
        def db_ping():
            try:
                with Session(self.engine) as session:
                    logger.debug("Trying to connect to database...")
                    session.query(text("1")).from_statement(text("SELECT 1")).all()  # type: ignore
                return MaybeConnected(value=True, error=None)
            except (exc.OperationalError, exc.ProgrammingError, RuntimeError) as oops:
                logger.warning("Connection to server failed: %s", str(oops))
                return MaybeConnected(value=None, error=oops)
        
        result = db_ping()
        next_poll = start_time + self.retry_time
        timeout_time = start_time + self.wait_for_server_time
        while not result.is_okay() and next_poll < timeout_time:
            logger.warning(
                f"Waiting for DB server. Will retry at {next_poll}.",
            )
            sleep_time = (next_poll - datetime.now()).total_seconds()
            if sleep_time > 0:
                time.sleep(sleep_time)
            next_poll += self.retry_time
            result = db_ping()
            
        return result

connection = Connection()

def get_db():
    session = Session(connection.engine)
    try:
        yield session
    finally:
        session.close()
