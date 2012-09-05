from dashboard.models import OfflineUser, User

class TestOfflineUser():
    def test_get_offline_pk(self):
        """
        Tests that OfflineUser.objects.get_offline_pk returns the correct value from an existing user 
        """
        offline_pk_from_db = OfflineUser.objects.get(user__username='sreenu').offline_pk_id
        offline_pk_id = OfflineUser.objects.get_offline_pk('sreenu', True)   
        print "pass" if offline_pk_id == offline_pk_from_db else "fail"
        
        offline_pk_id = OfflineUser.objects.get_offline_pk('development_manager', False)
        print "pass" if offline_pk_id is None else "fail"
        
        new_offline_pk = User.objects.get(username='development_manager').id*1000000000 + 1000
        offline_pk_id = OfflineUser.objects.get_offline_pk('development_manager', True)
        print "pass" if offline_pk_id == new_offline_pk else "fail"
        OfflineUser.objects.get(user__username='development_manager').delete()
    
    def test_set_offline_pk(self):
        """
         Tests that OfflineUser.objects.set_offline_pk sets value for the correct user correctly
        """
        old_offline_pk_from_db = OfflineUser.objects.get(user__username='sreenu').offline_pk_id
        val_offline_pk = old_offline_pk_from_db + 1
        success = OfflineUser.objects.set_offline_pk(val_offline_pk)
        if not success:
            print "fail"
        new_offline_user_from_db = OfflineUser.objects.get(user__username='sreenu')        
        print "pass" if new_offline_user_from_db.offline_pk_id == val_offline_pk else "fail"
