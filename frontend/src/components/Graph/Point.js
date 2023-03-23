export default class Point {
	constructor(id, name, x, y, outboundLineIndexs, inboundLineIndexes, fontColour) {
		this.id = id;
		this.name = name;
		this.outbound = outboundLineIndexs;
		this.inbound = inboundLineIndexes;
		this.fontColour = fontColour;
		this.x = x;
		this.y = y;
	}

	equals(point) {
		return this.id = point.id;
	}
}