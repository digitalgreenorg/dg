import { Component, OnInit } from '@angular/core';
import { environment } from '../../environments/environment.loop';

@Component({
  selector: 'app-navs',
  templateUrl: './navs.component.html',
  styleUrls: ['./navs.component.css']
})

export class NavsComponent implements OnInit {
  //used for collapse button
  public isCollapsed:boolean = false;
  navsConfig = environment.navsConfig;

  //initialize modules as false and toggle based on user configuration
  overall : false;
  recent : false;
  
  //keep track of nav switches and respective subnavs
  toggleNav = {};
  //dict with key as end nav and its corresponding containers
  containers = {};

  constructor() { }
  
  ngOnInit(): void {
    Object.keys(this.navsConfig.navs).forEach(nav => {
      let tempDict = {};
      tempDict['status'] = false;
      //check if subNavs exists and create respective container with default view flag as false
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
      
      //check for active link on nav bar and set status as true 
      if(this.navsConfig.navs[nav].hasOwnProperty('active')){
        this.toggleNav[nav].status = true;
        this.showContent(nav);
      }
    });
  }
  
  //function to return list of keys from a dictionary
  getDictKeys(dict) {
    return Object.keys(dict)
  }
  
  //function to set status as true for clicked nav item and rest as false 
  setNav(selectedItem : string) {
    Object.keys(this.toggleNav).forEach(nav => {
      this.toggleNav[nav].status = false
    });
    this.toggleNav[selectedItem].status = true;

    //set show content for navs with subNavs
    if((this.toggleNav[selectedItem].hasOwnProperty('subNavs'))){
       this.toggleNav[selectedItem].subNavs.forEach(subNav => {
        if(this.navsConfig.navs[selectedItem].subNavs[subNav].hasOwnProperty('active')) {
          this.showContent(subNav)
        }
      });
    }
    else {
      this.showContent(selectedItem);
    }
  }

  //function to set containers on view based on nav clicked(applicable for both manin nav and subNav)
  showContent(selectedNav) {
    Object.keys(this.containers).forEach(container => {
          this.containers[container].displayContent = false
    });
    this.containers[selectedNav].displayContent = true;
  } 
}
