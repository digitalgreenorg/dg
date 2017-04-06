import { Injectable } from '@angular/core';
import {Headers, Http} from '@angular/http';
import 'rxjs/add/operator/toPromise';
import 'rxjs/add/operator/map';
import { MyData } from './my-data';
import { DATA } from './our-data'

@Injectable()
export class TopBarDataService {
  // private headers = new Headers({'Content-Type':'application/json'});
  private webUrl = 'http://localhost:8000/training/testmethod/'
  constructor(private http: Http) { }

  getData():Promise<MyData []> {
    // return Promise.resolve(DATA);
    return this.http.get(this.webUrl)
            .toPromise()
            .then(response => response.json().data as MyData[])
            .catch(this.handleError);
  }

  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error); // for demo purposes only
    return Promise.reject(error.message || error);
  }

}
