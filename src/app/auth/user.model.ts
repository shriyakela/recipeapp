//to store data of user to know if the user is authenticated or not(validating if the token is still valid)
export class User{
    constructor(
        public email:string, 
        public id?:string, 
        // private _token:string, 
        // private _tokenExpirationDate: Date
    ){}

    //getter is a special type of property where we can write code that executes when the property is accessed
    //it cannot be overriden by assigning a value 
    // get token(){
    //     //if token has expired
    //     if(!this._tokenExpirationDate || new Date() > this._tokenExpirationDate){
    //         return null;
    //     }
    //     return this._token;

    // }
}