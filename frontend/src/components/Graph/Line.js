export default class Line {
	constructor(x1, y1, x2, y2, colour) {
		this.x1 = x1;
		this.y1 = y1;
		this.x2 = x2;
		this.y2 = y2;
		this.colour = colour;
	}

	equals(line) {
		return (
			this.x1 === line.x1 && this.y1 === line.y1 && this.x2 === line.x2 && this.y2 == line.y2
			||
			this.x1 === line.x2 && this.y1 === line.y2 && this.x2 === line.x1 && this.y2 === line.y1
		);
	}
}