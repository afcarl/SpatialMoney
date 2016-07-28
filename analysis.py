import numpy as np
from save.save_db_dic import BackUp
from save.import_data import import_data, import_suffixes
from collections import OrderedDict


# ------------------------------------------------||| MONEY TEST |||----------------------------------------------- #

class MoneyAnalysis(object):

    def __init__(self):

        self.money_threshold = .90

    def test_for_money_state(self, direct_exchange, indirect_exchange):

        money = -1

        # Money = 0?
        # type '0' should use direct exchange
        cond0 = direct_exchange[0] > self.money_threshold

        # type '1' should use indirect exchange
        cond1 = indirect_exchange[1] > self.money_threshold

        # type '2' should use direct exchange
        cond2 = direct_exchange[2] > self.money_threshold

        if (cond0 * cond1 * cond2) == 1:

            money = 0

        else:

            # Money = 1?
            cond0 = direct_exchange[0] > self.money_threshold
            cond1 = direct_exchange[1] > self.money_threshold
            cond2 = indirect_exchange[2] > self.money_threshold

            if (cond0 * cond1 * cond2) == 1:

                money = 1

            else:

                # Money = 2?
                cond0 = indirect_exchange[0] > self.money_threshold
                cond1 = direct_exchange[1] > self.money_threshold
                cond2 = direct_exchange[2] > self.money_threshold

                if (cond0 * cond1 * cond2) == 1:
                    money = 2

        return money

    def analyse(self, suffix):

        parameters, direct_exchange, indirect_exchange = import_data(suffix=suffix)
        money_timeline = np.zeros(parameters["t_max"])
        money = {0: 0, 1: 0, 2: 0, -1: 0}
        interruptions = 0 

        for t in range(parameters["t_max"]):

            money_t = self.test_for_money_state(direct_exchange=direct_exchange[t],
                                                indirect_exchange=indirect_exchange[t])
            money_timeline[t] = money_t  
            money[money_t] += 1

            if t > 0:

                cond0 = money_t == -1
                cond1 = money_timeline[t-1] != -1
                interruptions += cond0 * cond1

        results = \
            {"money": money,
             "interruptions": interruptions,
             "money_timeline": money_timeline}

        data_to_save = OrderedDict([
            ('a0', parameters["workforce"][0]),
            ('a1', parameters["workforce"][1]),
            ('a2', parameters["workforce"][2]),
            ('alpha', parameters["alpha"]),
            ('tau', parameters["tau"]),
            ('t_max', parameters["t_max"]),
            ('map_size', parameters["map_limits"]["width"]*parameters["map_limits"]["height"])])
        
        return data_to_save


# ------------------------------------------------||| Data Saver |||----------------------------------------------- #   

class DataSaver(object):
    
    def _init_(self):
        pass

    @classmethod    
    def save_data(cls, session):

        money_analysis = MoneyAnalysis()

        data = []
        suffixes = import_suffixes(session)

        for suffix in suffixes:

            result = money_analysis.analyse(suffix=suffix)

            data.append(result)

        cls.write(data)

    @classmethod
    def write(cls, data):

        backup = BackUp()
        backup.save(data)


                                    
                                    
        
         
        
        
        

        

       
        

# ------------------------------------------------||| MAIN  |||----------------------------------------------- #   



def main(suffix):

    m = MoneyAnalysis()
    results = m.analyse(suffix)
    m.save_data(results) 
    
if __name__ == "__main__":

    main(suffix="bhablfbrbh")
