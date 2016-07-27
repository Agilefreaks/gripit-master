class InvalidObserverException(Exception):
    def __init__(self):
        super(Exception, self).__init__('Can only add instances of Observer')
