""" Configurações de Gerador de Logs Global para o projeto """


import logging
from logging.handlers import RotatingFileHandler



class LoggerManager(object):
    
    def __init__(
        self, 
        name: str,
        log_file: str = "app.log",
        level: int = logging.INFO
    ):
        
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Se já não existirem adicona/cria os Handlers
        if not self.logger.handlers:

            

            file_handler = RotatingFileHandler(
                        log_file, 
                        maxBytes=5 * 1024 * 1024, 
                        backupCount=3
            )

            file_handler.setLevel(level)

            # Manipulador para console
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)

            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            # Adicionar handlers ao logger
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        """ Retorna o Logger final configurado """

        return self.logger
