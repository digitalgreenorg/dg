import { Component, OnInit } from '@angular/core';
import { environment } from '../../environments/environment.loop';

@Component({
  selector: 'app-navs',
  templateUrl: './navs.component.html',
  styleUrls: ['./navs.component.css']
})

export class NavsComponent implements OnInit {
  public isCollapsed:boolean = false;
  navs = []
  navsConfig = environment.navsConfig;
  constructor() { }

  ngOnInit() {
    Object.keys(this.navsConfig).forEach(nav => {
      if(this.navsConfig[nav].active){
        let active = true;
      }
      this.navs.push({
        'name': nav,
        'active': this.navsConfig[nav].active
      });
    })
  }

  ngAfterViewInit() {
    console.log(this.navs);
  }
  

}
