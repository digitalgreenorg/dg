import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
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
  constructor(private router: Router) {
    this.router.events.subscribe(route => {
            this.containers['Home'].displayContent = true;
            console.log(route['url']);
        });
  }
  
  ngOnInit() {
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

  showContent(selectedNav) {
    Object.keys(this.containers).forEach(container => {
          this.containers[container].displayContent = false
    });
    this.containers[selectedNav].displayContent = true;
  } 
}
