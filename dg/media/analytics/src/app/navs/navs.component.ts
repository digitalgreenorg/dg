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
  containers = {}

  constructor() {}
  
  /*ngOnInit() {
    let exceptionNavs = ['active','overall','recent','showDivs']
    Object.keys(this.navsConfig).forEach(navOne => {
      let tempDict = {}
      tempDict['status'] = false;
      tempDict['subNav'] = fillSubNav(this.navsConfig[navOne])
      this.toggleNav[navOne] = tempDict;
    })
     function fillSubNav(subNavs) {
      let navsList = []
      Object.keys(subNavs).forEach(nav => {
        if(!(exceptionNavs.indexOf(nav)>-1)) {
          navsList.push(nav);
        }
      });
      return navsList
    }
    console.log(this.toggleNav);
    console.log(this.containers);
  }

  showContent(nav,subNav) {
    this.containers = {}
    let contentDict = {}
    if(subNav != null){
      this.containers = this.navsConfig[nav][subNav]
    }
    else {
      this.containers = this.navsConfig[nav]
    }
    console.log(this.containers)
  }

  getDictKeys(dict) {
    return Object.keys(dict)
  }

  setNav(selectedItem : string) {
    Object.keys(this.toggleNav).forEach(nav => {
      this.toggleNav[nav].status = false
    });
    this.toggleNav[selectedItem].status = true;
    if(this.toggleNav[selectedItem].subNav.length == 0){
      this.showContent(selectedItem, null);
    }
  }*/
  ngOnInit() {
    Object.keys(this.navsConfig.navs).forEach(navOne => {
      let tempDict = {}
      tempDict['status'] = false;
      if(this.navsConfig.navs[navOne].subNavs != undefined){
        tempDict['subNavs'] = this.navsConfig.navs[navOne].subNavs;
      }
      else {
        tempDict['containers'] = this.navsConfig.navs[navOne].containers;
      }
      this.toggleNav[navOne] = tempDict;
    });
    console.log(this.toggleNav);
  }
  getDictKeys(dict) {
    return Object.keys(dict)
  }
  setNav(selectedItem : string) {
    Object.keys(this.toggleNav).forEach(nav => {
      this.toggleNav[nav].status = false
    });
    this.toggleNav[selectedItem].status = true;
    /*if(this.toggleNav[selectedItem].subNav.length == 0){
      this.showContent(selectedItem, null);
    }*/
  }
  showContent(nav,subNav) {
    this.containers = {}
    if(subNav != null){
      this.containers = this.navsConfig.navs[nav].subNavs[subNav]
    }
    else {
      this.containers = this.navsConfig.navs[nav]
    }
    console.log(this.containers)
  }
}
