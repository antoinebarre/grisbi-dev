import grisbi.stocks

# grisbi.stocks.save_value("GE",dataFolder="work/data")

# aa=grisbi.stocks.get_values_from_csv("GE",dataFolder="work\data")
# print(aa.tail())


grisbi.stocks.save_value("GE",dataFolder="work/data")
import grisbi.plot
grisbi.plot.plot_stock("GE",dataFolder="work/data")

# tt =grisbi.stocks.get_values_from_csv("toto")
# print(not tt.empty)
# grisbi.stocks.get_values_from_csv("GE",dataFolder="work/data")