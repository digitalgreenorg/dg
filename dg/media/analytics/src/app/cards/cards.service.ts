import { Injectable } from '@angular/core';
import { Headers, Http, URLSearchParams, RequestOptions } from '@angular/http';
import 'rxjs/add/operator/toPromise';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import { Observable } from 'rxjs/Rx';

@Injectable()
export class CardsService {

  constructor(private http: Http) { }

  getApiData(args): Observable<any> {

    let params: URLSearchParams = new URLSearchParams();
    for (let key in args.params) {
      params.set(key.toString(), args.params[key]);
    }

    let requestOptions: RequestOptions = new RequestOptions();
    requestOptions.search = params;
    return this.http.get(args.webUrl, requestOptions)
      .map(response => response.json())
      .catch(this.handleError);
  }
  private handleError(error: any): Observable<any> {
    console.error('An error occurred', error); // for demo purposes only
    return Observable.throw(error.json().error || 'Server error');
  }
}
