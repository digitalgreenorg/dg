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
/*    Object.keys(this.navsConfig.navs).forEach(nav => {
      let tempDict = {}
      tempDict['status'] = false;
      if(this.navsConfig.navs[nav].subNavs != undefined){
        tempDict['subNavs'] = this.navsConfig.navs[nav].subNavs;
      }
      else {
        tempDict['containers'] = this.navsConfig.navs[nav].containers;
      }
      this.toggleNav[nav] = tempDict;
    });*/
    Object.keys(this.navsConfig.navs).forEach(nav => {
      let tempDict = {};
      tempDict['status'] = false;
      if(this.navsConfig.navs[nav].subNavs != undefined){
        tempDict['subNavs'] = this.getDictKeys(this.navsConfig.navs[nav].subNavs);
        Object.keys(this.navsConfig.navs[nav].subNavs).forEach(subNav => {
          this.containers[subNav] = this.navsConfig.navs[nav].subNavs[subNav]
          this.containers[subNav]['displayContent'] = false;
        });
      }
      else {
        this.containers[nav] = this.navsConfig.navs[nav]
        this.containers[nav]['displayContent'] = false;
      }
      this.toggleNav[nav] = tempDict;
      //console.log(this.containers);
      //console.log(this.toggleNav)
    });

  }

  getDictKeys(dict) {
    return Object.keys(dict)
  }
  
  setNav(selectedItem : string) {
    Object.keys(this.toggleNav).forEach(nav => {
      this.toggleNav[nav].status = false
    });
    this.toggleNav[selectedItem].status = true;
    if(!(this.toggleNav[selectedItem].hasOwnProperty('subNavs'))){
      this.showContent(selectedItem);
    }
  }

/*  showContent(nav,subNav) {
    this.containers = {}
    if(subNav != null){
      this.containers = this.navsConfig.navs[nav].subNavs[subNav]
    }
    else {
      this.containers = this.navsConfig.navs[nav]
    }
    this.containers['displayContent'] = true
    console.log(this.containers);
  }*/

  showContent(selectedNav) {
    Object.keys(this.containers).forEach(container => {
          this.containers[container].displayContent = false
    });
    this.containers[selectedNav].displayContent = true;
    //console.log(this.toggleNav);
    console.log(this.containers);
  }

/*  showContent(selectedNav) {
    Object.keys(this.toggleNav).forEach(nav => {
        this.toggleNav[nav].status = false
    });
    if(this.toggleNav.hasOwnProperty(selectedNav)){
      this.toggleNav[selectedNav].status = true;
    }
    Object.keys(this.containers).forEach(container => {
          this.containers[container].displayContent = false
    });
    if(this.containers.hasOwnProperty(selectedNav)) {
      this.containers[selectedNav].displayContent = true;
    }
    console.log(this.toggleNav)
    console.log(this.containers)
  }*/
  
}
