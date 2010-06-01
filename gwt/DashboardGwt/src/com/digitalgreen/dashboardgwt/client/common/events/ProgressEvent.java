package com.digitalgreen.dashboardgwt.client.common.events;

import com.google.gwt.event.shared.EventHandler;
import com.google.gwt.event.shared.GwtEvent;

public class ProgressEvent extends GwtEvent<ProgressEvent.Handler> {
	
	private int progressMark = 0;
	public static final GwtEvent.Type<ProgressEvent.Handler> TYPE = new GwtEvent.Type<ProgressEvent.Handler>();
	
	public interface Handler extends EventHandler {
		public void onProgressEvent(ProgressEvent progressEvent);
	}

	public ProgressEvent(int progressMark) {
		this.progressMark = progressMark;
	}
	
	@Override
	protected void dispatch(Handler handler) {
		handler.onProgressEvent(this);
	}

	@Override
	public com.google.gwt.event.shared.GwtEvent.Type<Handler> getAssociatedType() {
		// TODO Auto-generated method stub
		return ProgressEvent.TYPE;
	}
	
	public int getProgressMark() {
		return this.progressMark;
	}
}