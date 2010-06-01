package com.digitalgreen.dashboardgwt.client.common.events;

import com.google.gwt.event.shared.HandlerManager;

/**
 * GWT event bus example: Alex Reid ar@phiz.net http://phiz.net
 *
 * Singleton instance to a HandlerManager instance. You could equally pass
 * a handlermanager instance around, rather than using a singleton.
 *
 * @author Alex Reid
 */
public class EventBus {
        private EventBus() {}
        private static final HandlerManager INSTANCE = new HandlerManager(null);
        public static HandlerManager get() {
                return INSTANCE;
        }
}