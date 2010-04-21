package com.digitalgreen.dashboardgwt.client.data.validation;

import java.util.ArrayList;

import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class UniqueConstraintValidator extends BaseValidator {
	private BaseData baseData = null;
	
	public UniqueConstraintValidator(ArrayList value, BaseData baseData) {
		super(value);
		this.baseData = baseData;
	}

	@Override
	public boolean validate() {
		BaseData.dbOpen();
		String query = "SELECT * FROM " + this.baseData.getTableName() + " WHERE ";
		ArrayList whereClause = ((ArrayList)this.getValue());
		// For composite unique indexes
		for(int i=0; i < whereClause.size(); i++) {
			ArrayList whereClausePart = (ArrayList)whereClause.get(i);
			query += (String)whereClausePart.get(0) + "='" + (String)whereClausePart.get(1) + "'"; 
			if(i != whereClause.size() - 1) {
					query += " AND ";
			}
		}
		query += ";";
		this.baseData.select(query);
		if (this.baseData.getResultSet().isValidRow()) {
			BaseData.dbClose();
			return false;
		}
		BaseData.dbClose();
		return true;
	}
}