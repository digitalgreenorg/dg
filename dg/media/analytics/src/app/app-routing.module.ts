import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { NavsComponent } from './navs/navs.component';

const routes: Routes = [
  { path: 'home', component: NavsComponent, pathMatch: 'full' },
/*  { path: 'home', data:{'nav':'Home'}},
  { path: 'analytics', data:{'nav':'Analytics'} },
  { path: 'time_series', data:{'nav':'Time Series'} }*/
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})

export class AppRoutingModule {}