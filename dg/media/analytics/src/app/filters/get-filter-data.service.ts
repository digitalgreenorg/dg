import { Injectable } from '@angular/core';
import { Http, RequestOptions, URLSearchParams } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';
import { config } from '../../config';

@Injectable()
export class GetFilterDataService {
  _baseUrl: string = config.url + "get_filter_data/";
  // private _request = new Request({
  //   method: 'GET',
  //   url: this._baseUrl
  // });

  constructor(private http: Http) { }

  getData(filters): Observable<any> {
    let params: URLSearchParams = new URLSearchParams();
    for (let key in filters) {
      params.set(key.toString(), filters[key]);
    }
    let requestOptions: RequestOptions = new RequestOptions();
    requestOptions.search = params;

    return this.http.get(this._baseUrl, requestOptions)
      .map(response => response.json())
      .catch(this.handleError);
  }

  getDataForParentFilter(filters): Observable<any> {
    let params: URLSearchParams = new URLSearchParams();
    for (let key in filters) {
      params.set(key.toString(), filters[key]);
    }
    let requestOptions: RequestOptions = new RequestOptions();
    requestOptions.search = params;

    return this.http.get(this._baseUrl, requestOptions)
      .map(response => response.json())
      .catch(this.handleError);
  }

  private handleError(error: any): Observable<any> {
    return Observable.throw(error.json().error || 'Server error');
  }
}
