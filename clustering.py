import matplotlib.pyplot as plt
import pandas as pd

from sklearn import decomposition
from sklearn import metrics
from sklearn import preprocessing

from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans


def hierarchicalClustering(data, sizes):
	"""
	Use ward clustering on the data
	"""

	min_max_scaler = preprocessing.MinMaxScaler()
	data_scaled = min_max_scaler.fit_transform(data)

	for k in sizes:
		print("Ward clustering with k = %i" % k)

		ward = AgglomerativeClustering(n_clusters=k, affinity="euclidean", linkage="ward")
		ward.fit_predict(data_scaled)
		cluster_labels = ward.labels_

		print(metrics.calinski_harabaz_score(data_scaled, cluster_labels))

		# Plot the clusters
		pca2D = decomposition.PCA(2) # Convert to 2 dimensions using PCA
		plot_columns = pca2D.fit_transform(data_scaled)
		plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1], c=cluster_labels) # Plot using a scatter plot and shade by cluster label
		plt.savefig("hierarchical_%s.png" % k) # Write to file
		plt.clf()

	return cluster_labels


def kMeansClustering(data, sizes):
	"""
	Use k-means clustering on the data
	"""

	min_max_scaler = preprocessing.MinMaxScaler()
	data_scaled = min_max_scaler.fit_transform(data)

	for k in sizes:
		print("K-Means clustering with k = %i..." % k)
		
		kmeans = KMeans(n_clusters=k)
		cluster_labels = kmeans.fit_predict(data_scaled)

		print(metrics.calinski_harabaz_score(data_scaled, cluster_labels))
		
		# Plot the clusters
		pca2D = decomposition.PCA(2) # Convert to 2 dimensions using PCA
		plot_columns = pca2D.fit_transform(data_scaled)
		plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1], c=cluster_labels) # Plot using a scatter plot and shade by cluster label
		plt.savefig("k-means_%s.png" % k) # Write to file
		plt.clf()

	return cluster_labels


def dbScanClustering(data, epss, min_spacing):
	"""
	Use ward clustering on the data
	"""

	min_max_scaler = preprocessing.MinMaxScaler()
	data_scaled = min_max_scaler.fit_transform(data)

	for eps in epss:
		print("DBScan clustering with eps = %f and min_samples = %i..." % (eps, min_spacing))
		clustering = DBSCAN(eps=eps, min_samples=min_spacing).fit(data_scaled)
		cluster_labels = clustering.labels_

		print(set(cluster_labels))
		print(metrics.calinski_harabaz_score(data_scaled, cluster_labels))
	'''
	# Plot the clusters
	pca2D = decomposition.PCA(2) # Convert to 2 dimensions using PCA
	plot_columns = pca2D.fit_transform(data_scaled)
	plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1], c=cluster_labels) # Plot using a scatter plot and shade by cluster label
	plt.savefig("dbscan_%s_%s.png" % (eps, min_spacing)) # Write to file
	plt.clf()
	'''
	return cluster_labels


if __name__ == "__main__":

	hist_data = pd.read_csv(".\\cleaned_data\\merged_data.csv")

	subset = hist_data[["all_td", "def_int_td", "fg_perc", "fga", "fgm", "kick_ret", "kick_ret_td", "kick_ret_yds",
						"kick_ret_yds_per_ret", "pass_adj_yds_per_att", "pass_att", "pass_cmp", "pass_cmp_perc",
						"pass_int", "pass_rating", "pass_sacked", "pass_sacked_yds", "pass_td", "pass_yds",
						"pass_yds_per_att", "punt_ret", "punt_ret_td", "punt_ret_yds", "punt_ret_yds_per_ret",
						"punt_yds_per_punt", "rec", "rec_td", "rec_yds", "rec_yds_per_rec", "rec_yds_per_tgt",
						"rush_att", "rush_td", "rush_yds", "rush_yds_per_att", "scoring", "targets", "two_pt_md",
						"xp_perc", "xpa", "xpm"]]
	
	sizes = [3]
	ward_labels = hierarchicalClustering(subset, sizes)
	hist_data["ward_labels"] = ward_labels
	
	sizes = [3]
	kmeans_labels = kMeansClustering(subset, sizes)
	hist_data["kmeans_labels"] = kmeans_labels
	
	epss = [0.3]
	min_spacing = 120
	dbscan_labels = dbScanClustering(subset, epss, min_spacing)
	hist_data["dbscan_labels"] = dbscan_labels

	hist_data.to_csv("merged_w_labels.csv")
	