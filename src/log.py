import logging
# Add the handler to logger
logging.basicConfig(filename='test.log',
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s')   
logger = logging.getLogger()  

def addKeywordfilter(keyword):
    for handler in logging.root.handlers:
        handler.addFilter(logging.Filter(keyword))
    logger=logging.getLogger() 

# Add the filter to the root logger

