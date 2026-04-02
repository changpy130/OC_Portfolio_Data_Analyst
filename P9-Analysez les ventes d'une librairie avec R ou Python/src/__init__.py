from .data_reader import load_customers, load_products, load_transactions, show_info, load_file_joined, load_b2b, load_b2c, load_all_clients, get_basic_kpis
from .analysis import ca, ca_moyenne_mobile
from .statistics import test_statistic, is_numeric
from .graph import plot_lorenz, plot_qq, plot_heatmap, plot_scatter, plot_boxplot