import { Injectable } from '@angular/core';
import { Http, Response, Request, Headers } from '@angular/http';

import { Observable } from 'rxjs/Observable';
import {Observer} from 'rxjs/Observer';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';

@Injectable()
export class GetFilterDataService {

  _baseUrl : string = "/training/get_filter_data";
  private _request = new Request({
    method: 'GET',
    url: this._baseUrl
  });

  data: any;

  constructor(private http: Http) { }

  getData(): Observable<any>{
    return this.http.get(this._baseUrl)
                    .map(response => response.json())
                    .catch(this.handleError);
  }

  private handleError(error: any): Observable<any> {
    console.error('An error occurred', error); // for demo purposes only
    return Observable.throw(error.json().error || 'Server error');
  }
}