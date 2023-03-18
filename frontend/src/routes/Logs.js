import { Link, NavLink, Outlet,redirect} from 'react-router-dom';
import { Container, Heading, VStack,Spinner } from '@chakra-ui/react';
import { useEffect, useMemo, useState } from 'react';
import Header from '../components/Header';
import { fetchLogs } from '../api';
import CustomTable from '../components/CustomTable';

const Logs = () => {
	const [logs, setLogs] = useState([]);
	const columns =useMemo(()=>
	{ 
		let orginal={
			'date':{
				header: 'Date',
			},
			'action':{
				header: 'Action',
				canFilter:true
			},
			'modelName':{
				header: 'Object Type',
				canFilter:true
			},
			'username':{
				header: 'Username',
				canFilter:true
			},
			'objectID':{
				header: 'ObjectID',
				canFilter:true,
				Cell:(rowID,value)=><Link to={`/${rowID.model_name}/${value}`} as={NavLink}>{value}</Link>
			}
		};
		return orginal;
	}
	,[]);
	useEffect(() => {
		fetchLogs().then(res=>setLogs(res.data));
	},[]);
	return (
		<CustomTable rows={logs} cols={columns}  setSelectedRows={()=>{}} preSelIDs={[]}/>
	);
};

export default Logs;
