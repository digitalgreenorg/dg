import { Injectable } from '@angular/core';
import { Headers, Http, URLSearchParams, RequestOptions } from '@angular/http';
import 'rxjs/add/operator/toPromise';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import { Observable } from 'rxjs/Rx';
import { config } from '../../config';

@Injectable()
export class GlobalFilterService {

  private graphURL = config.url + "get_global_filter_data/";

  constructor(private http: Http) { }

  getData(): Observable<any> {

    return this.http.get(this.graphURL)
      .map(response => response.json())
      .catch(this.handleError);
  }
  private handleError(error: any): any {
    return Observable.throw(error.json().error || 'Server error');
  }
}
