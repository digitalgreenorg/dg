import { Component, OnInit, Pipe, Inject } from '@angular/core';
import { DOCUMENT,Title } from '@angular/platform-browser';
import { environment } from '../environments/environment.training';

export var global_filter: any;

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: []
})

export class AppComponent implements OnInit {
  generalConfig = environment.generalConfig;
  constructor( @Inject(DOCUMENT) private document: any, private titleService: Title) {
    global_filter = this.parseUrl(this.document.location.href);
  }
  defaults: any;
  ngOnInit() :void {
    this.setTitle (this.generalConfig.title);
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

  public setTitle( newTitle: string) {
    this.titleService.setTitle( newTitle );
  }
}
