import { Box } from '@chakra-ui/react';

// install (please make sure versions match peerDependencies)
// yarn add @nivo/core @nivo/network
import { ResponsiveNetwork } from '@nivo/network';
import data from './mock_tags.json';
import { BasicTooltip } from '@nivo/tooltip';
const ToolTip= (props) => {
	return (
	  <BasicTooltip
			id={props.node.id}
			value={props.node.data.degree}
	  />
	);
};
const MyResponsiveNetwork = ({ data /* see data tab */ }) => (
	<ResponsiveNetwork
		data={data}
		margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
		linkDistance={100}
		linkColor={function(e){
			return e.data.linkColor;}}
		nodeSize={function(n){
			let size=25*n.size;
			if (size>50){
				return 50; 
			}
			return size;}}
		nodeColor={function(e){return e.color;}}
		linkThickness={1}
		nodeTooltip={ToolTip}
		onClick={(e)=>console.log(e)}
		centeringStrength={0.1}
		repulsivity={10}
	/>
);
const AsssetGraph = () => {
	return (<div style={{height: '1000px',width: '100vw'}}>
		<MyResponsiveNetwork data={data}/>
	</div> );
};
 
export default AsssetGraph;