export class Group{
    public name:string;
    public description:string;
    public imagePath:string;
    public isPublic: boolean;

    constructor(name:string, description:string, imagePath:string, isPublic:boolean){
        this.name = name;
        this.description = description;
        this.imagePath = imagePath;
        this.isPublic = isPublic;
    }

}