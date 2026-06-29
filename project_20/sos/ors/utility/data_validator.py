class DataValidator:

    @classmethod
    def is_not_null(self,val):
        if(val == None or val == "" ):
            return False
        else:
            return True

    @classmethod
    def is_null(self,val):
        if(val == None or val == "" ):
            return True
        else:
            return False