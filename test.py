import grisbi

grisbi.stocks.save_value("GE",dataFolder="work/data")

aa=grisbi.stocks.get_values_from_csv("titi",dataFolder="work\data")
print(aa.tail())