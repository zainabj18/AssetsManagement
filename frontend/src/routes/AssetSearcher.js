import { VStack } from '@chakra-ui/react';
import { Box } from '@chakra-ui/react';
import {Accordion,AccordionItem,AccordionButton,AccordionPanel,AccordionIcon} from '@chakra-ui/react';
import { Checkbox } from '@chakra-ui/react';

const FilterBasedSearch = () => {
	return (
		<Box p={30}>
			<VStack> <p>This is the Filter Based Search Page !!</p></VStack>
			<Accordion defaultIndex={[0]} allowMultiple>
				<AccordionItem>
					<h2>
						<AccordionButton>Asset Type
							<AccordionIcon />
						</AccordionButton>
					</h2>
					<AccordionPanel pb={4}>
						<VStack align = {'left'}>
							<Checkbox colorScheme='green' defaultChecked>Framework</Checkbox>
							<Checkbox colorScheme='green' defaultChecked>Documentation</Checkbox>
						</VStack>
					</AccordionPanel>
				</AccordionItem>
				<AccordionItem>
					<h2>
						<AccordionButton>
							Tags
							<AccordionIcon />
						</AccordionButton>
					</h2>
					<AccordionPanel pb={4}>
						<VStack align = {'left'}>
							<Checkbox colorScheme='green' defaultChecked>React</Checkbox>
						</VStack>
					</AccordionPanel>
				</AccordionItem>
				<AccordionItem>
					<h2>
						<AccordionButton>
							Projects
							<AccordionIcon />
						</AccordionButton>
					</h2>
					<AccordionPanel pb={4}>
						<VStack align = {'left'}>
							<Checkbox colorScheme='green' defaultChecked>Project A</Checkbox>
							<Checkbox colorScheme='green' defaultChecked>Project B</Checkbox>
							<Checkbox colorScheme='green' defaultChecked>Project C</Checkbox>
							<Checkbox colorScheme='green' defaultChecked>Project D</Checkbox>
						</VStack>
					</AccordionPanel>
				</AccordionItem>
				<AccordionItem>
					<h2>
						<AccordionButton>
							Access Levels
							<AccordionIcon />
						</AccordionButton>
					</h2>
					<AccordionPanel pb={4}>
						<VStack align = {'left'}>
							<Checkbox colorScheme='green' defaultChecked>Public</Checkbox>
							<Checkbox colorScheme='green' defaultChecked>Internal</Checkbox>
							<Checkbox colorScheme='green' defaultChecked>Restricted</Checkbox>
							<Checkbox colorScheme='green' defaultChecked>Confidential</Checkbox>
						</VStack>
					</AccordionPanel>
				</AccordionItem>
			</Accordion>
		</Box>
	);
  
};
export default FilterBasedSearch;
