from preprocess import Dataset
import math

class Worktable:
    def __init__(self):
        self.dataset = Dataset()
        self.dataset.get_data()
        self.volatility = None
    
    def cal_volatility(self):
        # we use e as the base when calculating the log return
        self.volatility = {}
        for inc_id in list(self.dataset.val_inc_set):
            log_return_list = []
            price_list = self.dataset.price_dict[inc_id]
            assert len(price_list)==72
            for t in range(len(price_list)-1):
                log_return = math.log(price_list[t+1]) - math.log(price_list[t])
                log_return_list.append(log_return)
            assert len(log_return_list)==71
            return_mean = sum(log_return_list) / len(log_return_list)
            vol = 0
            for r in log_return_list:
                vol += ( r - return_mean )**2
            vol = (vol/(len(log_return_list)-1))**0.5
            self.volatility[inc_id] = vol




if __name__ == '__main__' :
    w = Worktable()
    w.cal_volatility()
    print('volatility:\n',w.volatility)

