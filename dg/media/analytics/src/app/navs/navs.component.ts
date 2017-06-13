import { Component, OnInit } from '@angular/core';
import { environment } from '../../environments/environment.loop';

@Component({
  selector: 'app-navs',
  templateUrl: './navs.component.html',
  styleUrls: ['./navs.component.css']
})

export class NavsComponent implements OnInit {
  public isCollapsed:boolean = false;
  navsFirst = [];
  navsSecond = [];
  overall : false;
  recent : false;
  navsConfig = environment.navsConfig;
  constructor() { }

  ngOnInit() {
    Object.keys(this.navsConfig).forEach(navOne => {
      this.navsFirst.push({
        'name': navOne,
        'data-target': '#'+navOne,
        'active': this.navsConfig[navOne].active
      });
      Object.keys(this.navsConfig[navOne]).forEach(navTwo => {
        this.navsSecond.push({
          'id': navOne,
          'name':navTwo,
          'active':this.navsConfig[navOne][navTwo].active
        })
      });
    });
  }

  ngAfterViewInit() {
    console.log(this.navsFirst);
    console.log(this.navsSecond);
  }
  

}
