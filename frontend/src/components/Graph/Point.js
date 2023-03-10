export default class Point {
	constructor(id, name, x, y, outboundLineIndexs, inboundLineIndexes) {
		this.id = id;
		this.name = name;
		this.outbound = outboundLineIndexs;
		this.inbound = inboundLineIndexes;
		this.x = x;
		this.y = y;
	}

	equals(point) {
		return this.id = point.id;
	}

	getTransform() {
		return 'translate(' + this.x + 'px, ' + this.y + 'px)';
	}
}