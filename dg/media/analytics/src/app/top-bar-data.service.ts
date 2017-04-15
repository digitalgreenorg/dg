import { Injectable } from '@angular/core';
import {Headers, Http, URLSearchParams, RequestOptions } from '@angular/http';
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
    
    let params : URLSearchParams = new URLSearchParams();
    params.set('start_date', '2015-01-01');
    params.set('end_date', '2017-04-15');
    let requestOptions : RequestOptions = new RequestOptions();
    requestOptions.search = params;
    return this.http.get(this.webUrl, requestOptions)
            .toPromise()
            .then(response => response.json() as MyData[])
            .catch(this.handleError);
  }

  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error); // for demo purposes only
    return Promise.reject(error.message || error);
  }

}
// header("Access-Control-Allow-Origin: *");