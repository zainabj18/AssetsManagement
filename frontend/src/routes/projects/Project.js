import { Box, Flex, HStack, Input, useBoolean, VStack, } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { Outlet, useOutletContext } from 'react-router-dom';
import { fetchProjects } from '../../api';
import CustomNavLink from '../../components/CustomNavLink';
import CreateProject from '../../components/CreateProject';

const Projects = () => {
	const [projects, setProjects] = useState([]);
	const [results, setResults] = useState([]);
	const [trigger, setTrigger] = useBoolean();
	const [update, setUpdate] = useBoolean();
	//trigger refresh of projetcs on create

	const filter = (value) => {
		if (value === '') {
			setResults(projects);
		} else {
			let filteredProject = projects.filter((t) => t.projectName.toLowerCase().includes(value.toLowerCase()));
			setResults(filteredProject);
		}
	};

	useEffect(() => {
		fetchProjects().then((res) => {
			setProjects(res.data);
			setResults(res.data);
		}
		);
	}, [trigger, update]);

	return (<Box w='75vw' minH='80vh' display={'flex'} flexDirection="row" p={2} border alignSelf={'center'}>
		<Box w='30%' minH='100%' bg='gray.300' p={4} color='black' align={'top'}>
			<HStack>
				<Input type='text' placeholder='Search for project ...' onChange={(e) => { filter(e.target.value); }} />
				<CreateProject trigger={setTrigger} />
			</HStack>
			<VStack p={2}>
				{results.map((t, index) => (
					<CustomNavLink key={index} to={`./${t.projectID}`} w='100%'>
						{t.projectName}
					</CustomNavLink>

				))}

			</VStack>
		</Box>
		<Box w='62%' minH='100%' bg='white'>
			<Outlet context={[update, setUpdate]} />
		</Box>
	</Box>
	);
};

export default Projects;
