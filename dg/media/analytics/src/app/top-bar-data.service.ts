import { Injectable } from '@angular/core';
import {Headers, Http, URLSearchParams, RequestOptions } from '@angular/http';
import 'rxjs/add/operator/toPromise';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import { MyData } from './my-data';
import { DATA } from './our-data'
import { Observable } from 'rxjs/Rx'

@Injectable()
export class TopBarDataService {
  // private headers = new Headers({'Content-Type':'application/json'});
  private webUrl = 'http://localhost:8000/training/testmethod/'
  // private 
   
  constructor(private http: Http) { }
  getData():Observable<MyData []> {
    
    let params : URLSearchParams = new URLSearchParams();
    params.set('start_date', '2015-01-01');
    params.set('end_date', '2017-04-15');
    let requestOptions : RequestOptions = new RequestOptions();
    requestOptions.search = params;
    return this.http.get(this.webUrl, requestOptions)
            .map(response => response.json() as MyData[])
            .catch(this.handleError);
  }

  private handleError(error: any): Observable<any> {
    console.error('An error occurred', error); // for demo purposes only
    return Observable.throw(error.json().error || 'Server error');
    // return Promise.reject(error.message || error);
  }

  // getGraphData():Promise<any>{
  //   // return this.http.get()
  // }

}
// header("Access-Control-Allow-Origin: *");