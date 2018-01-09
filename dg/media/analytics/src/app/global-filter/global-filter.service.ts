import { Injectable } from '@angular/core';
import { Headers, Http, URLSearchParams, RequestOptions } from '@angular/http';
import 'rxjs/add/operator/toPromise';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import { Observable } from 'rxjs/Rx';
import { config } from '../../config';
import { global_filter } from '../app.component';

@Injectable()
export class GlobalFilterService {

  // private graphURL = config.url + "get_global_filter_data/";
  private graphURL = "get_global_filter_data/";

  constructor(private http: Http) { }

  getData(url = this.graphURL): Observable<any> {
    let params: URLSearchParams = new URLSearchParams();

    for (let key in global_filter) {
      params.set(key, global_filter[key]);
    }

    let requestOptions: RequestOptions = new RequestOptions();
    requestOptions.search = params;
    // console.log(config.url + url + '/?' + params);
    return this.http.get(config.url + url, requestOptions)
      .map(response => response.json())
      .catch(this.handleError);
  }
  private handleError(error: any): any {
    return Observable.throw(error.json().error || 'Server error');
  }
}
