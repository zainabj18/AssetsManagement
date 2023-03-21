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
		linkDistance={50}
		linkColor={function(e){
			return e.data.linkColor;}}
		nodeSize={function(n){return n.size;}}
		activeNodeSize={function(n){return 1.5*n.size;}}
		nodeColor={function(e){return e.color;}}
		nodeBorderWidth={1}
		nodeTooltip={ToolTip}
		onClick={(e)=>console.log(e)}
	/>
);
const AsssetGraph = () => {
	return (<div style={{height: '100vh',width: '100vw'}}>
		<MyResponsiveNetwork data={data}/>
	</div> );
};
 
export default AsssetGraph;