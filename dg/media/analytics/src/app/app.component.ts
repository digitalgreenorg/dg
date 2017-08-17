import { Component, OnInit, Pipe, Inject } from '@angular/core';
import { DOCUMENT } from '@angular/platform-browser';

export var global_filter: any;

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: []
})

export class AppComponent {

  constructor( @Inject(DOCUMENT) private document: any) {
    global_filter = this.parseUrl(this.document.location.href);
  }

  private parseUrl(url): any {
    let param = url.split('?');
    let res = {}
    let splitArray: any;
    if (param[1]) {
      let params = param[1].split('&');
      for (let obj of params) {
        splitArray = obj.split('=');
        res[splitArray[0]] = splitArray[1];
      }
    }
    return res;
  }
}
