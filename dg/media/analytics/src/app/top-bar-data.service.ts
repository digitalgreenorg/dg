import { Injectable } from '@angular/core';
import { Headers, Http, URLSearchParams, RequestOptions } from '@angular/http';
import 'rxjs/add/operator/toPromise';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import { Observable } from 'rxjs/Rx';
import { Config } from './config/config';

@Injectable()
export class TopBarDataService {

  constructor(private http: Http) { }

  getApiData(args):Observable<Config> {

    let params : URLSearchParams = new URLSearchParams();
    if (args.params.start_date != null)
      params.set('start_date', args.params.start_date);
    if (args.params.end_date != null)
      params.set('end_date', args.params.end_date);
    params.set('trainer',args.params.Trainer);
    params.set('state',args.params.State);
    params.set('apply_filter', args.params.apply_filter);
    let requestOptions : RequestOptions = new RequestOptions();
    requestOptions.search = params;
    return this.http.get(args.webUrl, requestOptions)
            .map(response => response.json()as Config)
            .catch(this.handleError);
  }
  private handleError(error: any): Observable<any> {
    console.error('An error occurred', error); // for demo purposes only
    return Observable.throw(error.json().error || 'Server error');
  }

}
// header("Access-Control-Allow-Origin: *");
