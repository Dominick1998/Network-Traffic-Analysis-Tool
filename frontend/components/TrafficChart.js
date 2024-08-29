import React, { useRef, useEffect } from 'react';
import * as d3 from 'd3';

const TrafficChart = ({ trafficData }) => {
  const chartRef = useRef();

  useEffect(() => {
    // Set up the chart dimensions and margins
    const margin = { top: 20, right: 30, bottom: 40, left: 50 };
    const width = 800 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    // Set up the SVG element
    const svg = d3.select(chartRef.current)
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Set up the x-scale and y-scale
    const x = d3.scaleTime().range([0, width]);
    const y = d3.scaleLinear().range([height, 0]);

    // Parse the date and set the domains
    const parseTime = d3.timeParse('%Y-%m-%dT%H:%M:%S.%LZ');
    trafficData.forEach(d => {
      d.timestamp = parseTime(d.timestamp);
    });
    x.domain(d3.extent(trafficData, d => d.timestamp));
    y.domain([0, d3.max(trafficData, d => d.length)]);

    // Create the line generator
    const line = d3.line()
      .x(d => x(d.timestamp))
      .y(d => y(d.length));

    // Append the line to the SVG element
    svg.append('path')
      .datum(trafficData)
      .attr('fill', 'none')
      .attr('stroke', 'steelblue')
      .attr('stroke-width', 1.5)
      .attr('d', line);

    // Add the x-axis
    svg.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x));

    // Add the y-axis
    svg.append('g')
      .call(d3.axisLeft(y));
  }, [trafficData]);

  return (
    <svg ref={chartRef}></svg>
  );
};

export default TrafficChart;
