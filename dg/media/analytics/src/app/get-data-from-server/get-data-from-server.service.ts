import { Injectable } from '@angular/core';
import { Http, Response, Request, Headers } from '@angular/http';

import { Observable } from 'rxjs/Observable';
import {Observer} from 'rxjs/Observer';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';

@Injectable()
export class GetDataFromServerService {
  // _baseUrl : string = "http://currentmillis.com/time/minutes-since-unix-epoch.php";
  // _baseUrl : string = "http://www.digitalgreen.org/loop/total_static_data/";
  _baseUrl : string = "http://data.colorado.gov/resource/4ykn-tg5h.json";
  private _request = new Request({
    method: 'GET',
    url: this._baseUrl
  });

  data: JSON;

  constructor(private http: Http) { }

  getData(): Observable<JSON>{
    return this.http.get(this._baseUrl,{headers: this.getHeaders()}).map(this.extractData).catch(this.handleError);
  }

  private extractData(res: Response) {
    console.log("In Service");
    console.log(res);
    let body = res.json();
    this.data = body;
    return body.data || { };
  }

  private handleError (error: Response | any) {
      let errMsg: string;
      if (error instanceof Response) {
        const body = error.json() || '';
        const err = body.error || JSON.stringify(body);
        console.log(err);
        errMsg = `${error.status} - ${error.statusText || ''} ${err}`;
      } else {
        errMsg = error.message ? error.message : error.toString();
      }
      console.error(errMsg);
      return Observable.throw(errMsg);
    }

    private getHeaders(){
    let headers = new Headers();
    headers.append('Accept', 'application/json');
    return headers;
  }


}
