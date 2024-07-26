import { HttpInterceptorFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  // debugger
  // const myToken = localStorage.getItem('authToken');

  // const cloneRequest = req.clone({
  //   setHeaders:{
  //     Authorization: `Bearer ${myToken}`
  //   }
  // });
  // return next(cloneRequest);
  const myToken = localStorage.getItem('authToken');
  
  if (myToken) {
    const cloneRequest = req.clone({
      setHeaders: {
        Authorization: `Bearer ${myToken}`
      }
    });
    return next(cloneRequest);
  } else {
    console.warn('No auth token found.');
    return next(req);
  }
};
