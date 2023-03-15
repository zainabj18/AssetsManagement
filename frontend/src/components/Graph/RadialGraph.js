import { useEffect, useState } from 'react';
import Line from './Line';
import Point from './Point';
import Rotation from './Rotation';
import PointElement from './PointElement';
import { HStack, VStack, Text } from '@chakra-ui/react';

const RadialGraph = ({
	data = { points: [], joins: [] },
	size = 600,
	radiusPercent = 0.6,
	textSize = 15,
	backgroundColour = null,
	curveOffset = 1,
	fontColour = 'black',
	highightColour = 'grey',
	defaultColour = 'black',
	outboundColour = 'red',
	inboundColour = 'blue',
	twoWayColour = 'purple',
	defaultLineWidth = 1,
	highlightedLineWidth = 2,
	graphClearanceSpace = 15,
	show2WayInKey = true
}) => {

	const radius = size * radiusPercent / 2;
	const center = radius / radiusPercent;
	const angleSplit = Math.PI * 2 / data.points.length;

	useEffect(() => {
		onLoad();
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);

	const getX = (index) => {
		return center + radius * Math.sin(index * angleSplit);
	};

	const getY = (index) => {
		return center - radius * Math.cos(index * angleSplit);
	};

	const getRotation = (index) => {
		let rotation = index * angleSplit;
		let flipped = rotation > Math.PI;
		if (!flipped) {
			rotation -= Math.PI;
		}
		return new Rotation(rotation + Math.PI / 2, flipped);
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
				let line = new Line(getX(index), getY(index), getX(pointIndexes[to]), getY(pointIndexes[to]), defaultColour, defaultLineWidth);
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
			points.push(new Point(point.id, point.name, getX(index), getY(index), outbounds[point.id], inbounds[point.id], fontColour));
		});

		setPoints(points);
		setLines(lines);
	};

	const highightLines = (point, hovered) => {
		point.fontColour = (hovered) ? highightColour : fontColour;

		let l = [...lines];
		point.outbound.forEach(lineIndex => {
			l[lineIndex].colour = ((hovered) ? outboundColour : defaultColour);
			l[lineIndex].width = ((hovered) ? highlightedLineWidth : defaultLineWidth);
		});
		point.inbound.forEach(lineIndex => {
			if (l[lineIndex].colour === outboundColour) {
				l[lineIndex].colour = twoWayColour;
			}
			else {
				l[lineIndex].colour = ((hovered) ? inboundColour : defaultColour);
				l[lineIndex].width = ((hovered) ? highlightedLineWidth : defaultLineWidth);
			}
		});
		setLines(l);
	};

	return (
		<VStack>
			<HStack>
				<Text style={{ backgroundColor: outboundColour, height: '20px', width: '20px' }}>{' '}</Text><Text>Outbound</Text>
				<Text style={{ backgroundColor: inboundColour, height: '20px', width: '20px' }}>{' '}</Text><Text>Inbound</Text>
				{show2WayInKey && <><Text style={{ backgroundColor: twoWayColour, height: '20px', width: '20px' }}>{' '}</Text><Text>2 Way</Text></>}
			</HStack>
			<div style={{
				display: 'inline-block',
				height: size + 'px',
				width: size + 'px',
				backgroundColor: backgroundColour
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
								strokeWidth={line.width}
								strokeLinecap="round"
								fill="transparent"
							>
							</path>
						);
					})}
				</svg>
				{points.map((point, index) => {
					return (
						<PointElement
							point={point}
							key={index}
							onMouseOver={() => highightLines(point, true)}
							onMouseLeave={() => highightLines(point, false)}
							rotation={getRotation(index)}
							textSize={textSize}
							spacing={graphClearanceSpace}
						/>
					);
				})}
			</div>
		</VStack>
	);
};

export default RadialGraph;