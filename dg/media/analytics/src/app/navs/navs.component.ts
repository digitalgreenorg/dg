import { Component, OnInit } from '@angular/core';
import { environment } from '../../environments/environment.loop';

@Component({
  selector: 'app-navs',
  templateUrl: './navs.component.html',
  styleUrls: ['./navs.component.css']
})

export class NavsComponent implements OnInit {
  public isCollapsed:boolean = false;
  navsConfig = environment.navsConfig;
  overall : false;
  recent : false;
  toggleNav = {};
  containers = {};
  constructor() {}
  
  ngOnInit() {
    Object.keys(this.navsConfig.navs).forEach(nav => {
      let tempDict = {}
      tempDict['status'] = false;
      if(this.navsConfig.navs[nav].subNavs != undefined){
        tempDict['subNavs'] = this.navsConfig.navs[nav].subNavs;
      }
      else {
        tempDict['containers'] = this.navsConfig.navs[nav].containers;
      }
      this.toggleNav[nav] = tempDict;
    });
  }

  getDictKeys(dict) {
    return Object.keys(dict)
  }
  
  setNav(selectedItem : string) {
    this.containers['displayContent'] = false;
    Object.keys(this.toggleNav).forEach(nav => {
      this.toggleNav[nav].status = false
    });
    this.toggleNav[selectedItem].status = true;
    if(!(this.toggleNav[selectedItem].hasOwnProperty('subNavs'))){
      this.showContent(selectedItem, null);
    }
  }

  showContent(nav,subNav) {
    this.containers = {}
    if(subNav != null){
      this.containers = this.navsConfig.navs[nav].subNavs[subNav]
    }
    else {
      this.containers = this.navsConfig.navs[nav]
    }
    this.containers['displayContent'] = true
  }
}
