import { Badge } from '@chakra-ui/react';
import { useEffect, useMemo } from 'react';
import { Link as NavLink } from 'react-router-dom';
import CustomTable from '../CustomTable';
import {Link } from '@chakra-ui/react';
const AssetTable = ({assets,setSelectedAssets,preSelIDs,cols}) => {
	const columns =useMemo(()=>
	{ 
		let orginal={
			'assetID':{
				header: 'Asset ID',
				canFilter:true,
				Cell:(rowID,value)=><Link to={`/assets/${value}`} as={NavLink}>{value}</Link>
			},
			'name':{
				header: 'Asset Name',
				canFilter:true
			},
			'type_name':{
				header: 'Asset Type',
				canFilter:true
			},
			'classification':{
				header: 'Asset Classification',
				canFilter:true,
				Cell:(row,value)=>{return <Badge bg={value} color={'white'}>{value}</Badge>;}
			},
		};
		if (cols){
			orginal={...orginal,...cols};
		}
		return orginal;
	}
	,[cols]);
	useEffect(() => {

	},[assets,cols]);
	return (

		<CustomTable rows={assets} cols={columns}  setSelectedRows={setSelectedAssets} preSelIDs={preSelIDs}/>);
};
 
export default AssetTable;