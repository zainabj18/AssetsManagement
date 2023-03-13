import { useEffect, useState } from 'react';
import Line from './Line';
import Point from './Point';

const RadialGraph = ({
	data,
	size = 400,
	textSize = 15,
	curveOffset = 1,
	defaultColour = 'black',
	outboundColour = 'red',
	inboundColour = 'blue',
	twoWayColour = 'purple'
}) => {

	const radius = size / 2;
	const center = radius;
	const angleSplit = Math.PI * 2 / data.points.length;

	useEffect(() => {
		onLoad();
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);

	const getY = (index) => {
		return -radius * Math.cos(index * angleSplit) + center;
	};

	const getX = (index) => {
		return radius * Math.sin(index * angleSplit) + center;
	};

	const setCurve = (line) => {
		let offx = ((curveOffset * center) + ((line.x2 + line.x1) * 0.5)) / (curveOffset + 1);
		let offy = ((curveOffset * center) + ((line.y2 + line.y1) * 0.5)) / (curveOffset + 1);
		return 'M' + line.x1 + ' ' + line.y1 + ' Q ' + offx + ' ' + offy + ' ' + line.x2 + ' ' + line.y2;
	};

	const [lines, setLines] = useState([]);
	const [points, setPoints] = useState([]);

	const getIndex = (item, list) => {
		let index;
		for (index = 0; index < list.length; index++) {
			if (item.equals(list[index])) {
				return index;
			}
		}
		return -1;
	};

	const onLoad = () => {
		let pointIndexes = {};
		let inbounds = {};
		let outbounds = {};
		data.points.forEach((point, index) => {
			pointIndexes[point.id] = index;
			inbounds[point.id] = [];
			outbounds[point.id] = [];
		});

		let lines = [];
		data.joins.forEach((join, index) => {
			let out = [];
			join.to.forEach((to) => {
				let line = new Line(getX(index), getY(index), getX(pointIndexes[to]), getY(pointIndexes[to]), defaultColour);
				if (getIndex(line, lines) === -1) {
					lines.push(line);
				}
				let lineIndex = getIndex(line, lines);
				inbounds[to].push(lineIndex);
				out.push(lineIndex);
			});
			outbounds[join.from] = out;
		});

		let points = [];
		data.points.forEach((point, index) => {
			points.push(new Point(point.id, point.name, getX(index), getY(index), outbounds[point.id], inbounds[point.id]));
		});

		setPoints(points);
		setLines(lines);
	};

	const highightLines = (point, hovered) => {
		let l = [...lines];
		point.outbound.forEach(lineIndex => {
			l[lineIndex].colour = ((hovered) ? outboundColour : defaultColour);
		});
		point.inbound.forEach(lineIndex => {
			if (l[lineIndex].colour === outboundColour) {
				l[lineIndex].colour = twoWayColour;
			}
			else {
				l[lineIndex].colour = ((hovered) ? inboundColour : defaultColour);
			}
		});
		setLines(l);
	};

	return (
		<div style={{
			display: 'inline-block',
			height: size + 'px',
			width: size + 'px',
			backgroundColor: 'yellow'
		}}>
			<svg
				style={{
					position: 'absolute',
					height: size + 'px',
					width: size + 'px'
				}}
			>
				{lines.map((line, index) => {
					return (
						<path
							key={index}
							d={setCurve(line)}
							stroke={line.colour}
							strokeWidth='1'
							strokeLinecap="round"
							fill="transparent">
						</path>
					);
				})}
			</svg>
			{points.map((point, index) => {
				return (
					<h1
						key={index}
						style={{
							position: 'absolute',
							transform: point.getTransform(),
							fontSize: textSize
						}}
						onMouseOver={() => highightLines(point, true)}
						onMouseLeave={() => highightLines(point, false)}
					>
						{point.name}
					</h1>
				);
			})}
		</div>
	);
};

export default RadialGraph;