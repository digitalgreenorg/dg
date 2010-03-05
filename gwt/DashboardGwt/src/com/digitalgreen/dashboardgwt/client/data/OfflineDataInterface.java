package com.digitalgreen.dashboardgwt.client.data;

interface OfflineDataInterface {
	public void select(String selectSql, String ...args);
	public void insert(String insertSql, String ...args);
	public void delete(String deleteSql, String ...args);
	public void update(String updateSql, String ...args);
}