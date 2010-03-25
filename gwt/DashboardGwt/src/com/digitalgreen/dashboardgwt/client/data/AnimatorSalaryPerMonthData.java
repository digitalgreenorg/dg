package com.digitalgreen.dashboardgwt.client.data;

import com.digitalgreen.dashboardgwt.client.common.RequestContext;

public class AnimatorSalaryPerMonthData extends BaseData{

	protected static String tableID = "19";
	protected static String createTable = "CREATE TABLE IF NOT EXISTS `animator_salary_per_month` " +
												"(id INTEGER PRIMARY KEY NOT NULL ," +
												"animator_id INT  NOT NULL DEFAULT 0," +
												"DATE DATE  NOT NULL ," +
												"TOTAL_SALARY FLOAT(0,0)  NULL DEFAULT NULL," +
												"PAY_DATE DATE  NULL DEFAULT NULL, " +
												"FOREIGN KEY(animator_id) REFERENCES animator(id));";
	
	protected static String saveAnimatorSalaryPerMonthOfflineURL = "/dashboard/saveanimatorsalarypermonthoffline/";
	
	public AnimatorSalaryPerMonthData(){
		super();
	}
	
	@Override
	protected String getTableId() {
		return AnimatorSalaryPerMonthData.tableID;
	}
}