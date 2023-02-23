import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {fetchRelatedTags } from '../../api';

import ProjectSelect from '../../components/ProjectSelect';
const Projects = () => {
	const { id } = useParams();
	const [assetsin, setAssets] = useState([]);
	const link_col={'count':{
		header: 'Projects in Common',
		canFilter:true,
	}};

	useEffect(() => {
		fetchRelatedTags(id).then((data)=>{ console.log(data.data);
			setAssets(data.data);});
	}, [])
	;
	return (<ProjectSelect assets={assetsin} setSelectedAssets={()=>{}} preSelIDs={[]} cols={link_col}/>);
};
 
export default Projects;